# Text-Extraction-from-images-OCR-

To run this application, simply execute the app.py file. Then, navigate to http://127.0.0.1:5000 in your web browser and start uploading your images. The techniques used are:

Pyterrest is likely a custom or specialized tool for image search and retrieval. While specific details about the models used by Pyterrest are not widely known, such tools typically utilize:

    Convolutional Neural Networks (CNNs): For image feature extraction and analysis.
    Pre-trained models: Such as ResNet, VGG, or Inception, for identifying and categorizing objects within images.
    These models help in accurately retrieving similar images based on visual content.

easyocr uses a combination of advanced deep learning models to perform OCR. Specifically, it employs:

    Convolutional Neural Networks (CNNs): For detecting text regions within images.
    Recurrent Neural Networks (RNNs): For sequence prediction and recognizing text within detected regions.
    CRNN (Convolutional Recurrent Neural Network): A model that combines CNNs and RNNs to effectively handle both image feature extraction and sequential text recognition, making it robust for various languages and scripts.

ocrmypdf integrates several OCR engines to add text layers to PDFs. The primary model used is:

    Tesseract OCR: An open-source OCR engine developed by Google. Tesseract uses LSTM (Long Short-Term Memory) networks, which are a type of Recurrent Neural Network (RNN) suitable for recognizing text in images. This enables it to handle different fonts and styles within scanned documents, ensuring high accuracy in text recognition.
