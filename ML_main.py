from ML_Framework.Training.Prepare_training_dataset import extract_training_data
from ML_Framework.Training.data_gathering import collect_urls_into_csv
from ML_Framework.Training.Train_Model import train_model, train_model_all


if __name__=="__main__":
	# Merge urls files with label
	# collect_urls_into_csv()

	# Preapare training dataset
	extract_training_data()

	# Train ML model
	train_model_all()

	pass


