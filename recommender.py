import os
import spacy



# Train doc2vec on a list of tagged documents.

# This, in theory, will let us train on either a Roam journal
#   or a documents folder. 

# Ultimately, the model will be used to find KNN for a particular document.
# So each document will be assigned a TopicBoy Unique ID (TUID) for lookup
#   of the recommended item.



