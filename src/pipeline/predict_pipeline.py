from spacy.lang.en import English
import tensorflow as tf
import pickle
from sklearn.preprocessing import OneHotEncoder

def split_chars(text):
  return " ".join(list(text))

def import_assets():
    # Load the model
    model = tf.keras.models.load_model('assets/model.keras')
    
    # Load the label encoder
    f = open("assets/labelencoder", "rb")
    label_encoder = pickle.load(f)
    f.close()
    
    return model, label_encoder

def predict_output(abstract):

  # Setup english sentence parser
  nlp = English()

  # Create sentence splitting pipeline object
  nlp.add_pipe('sentencizer')

  # Create doc of parsed sequences
  doc = nlp(abstract)

  # Return detected sentences from doc in string typpe
  abstract_lines = [str(sent) for sent in list(doc.sents)]

  # Get total number of lines
  total_lines_in_sample = len(abstract_lines)

  # Loop through each line in the abstract and create a list of dictionaries containing features
  sample_lines = []
  for i , line in enumerate(abstract_lines):
    sample_dict = {}
    sample_dict['text'] = str(line)
    sample_dict['line_number'] = i
    sample_dict['total_lines'] = total_lines_in_sample - 1
    sample_lines.append(sample_dict)

  # Get all line number and total lines numbers then one hot encode them
  abstract_line_numbers = [line['line_number'] for line in sample_lines]
  abstract_total_lines = [line['total_lines'] for line in sample_lines]

  abstract_line_numbers_one_hot = tf.one_hot(abstract_line_numbers , depth = 15)
  abstract_total_lines_one_hot = tf.one_hot(abstract_total_lines , depth = 20)

  # Split the lines into characters
  abstract_chars = [split_chars(sentence) for sentence in abstract_lines]

  model, label_encoder = import_assets()

  # Making prediction on sample features
  abstract_pred_probs = model.predict(x = (abstract_line_numbers_one_hot,
                                           abstract_total_lines_one_hot,
                                           tf.constant(abstract_lines) ,
                                           tf.constant(abstract_chars),
                                           ))

  # Turn prediction probs to pred class
  abstract_preds = tf.argmax(abstract_pred_probs , axis = 1)

  # Prediction class integers into string class name
  abstract_pred_classes = [label_encoder.classes_[i] for i in abstract_preds]

  # Prints out the abstract lines and the predicted sequence labels
  return abstract_lines, abstract_pred_classes