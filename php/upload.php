<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_FILES["fileInput"])) {
    $targetDir = "/data/uploads";  // Directory where uploaded files will be saved
    $targetFile = $targetDir . basename($_FILES["fileInput"]["name"]);
    $uploadOk = 1;
    $imageFileType = strtolower(pathinfo($targetFile,PATHINFO_EXTENSION));
    
    // Check if image file is a actual image or fake image
    $check = getimagesize($_FILES["fileInput"]["tmp_name"]);
    if($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
    
    // Check if file already exists
    if (file_exists($targetFile)) {
        echo "Sorry, file already exists.";
        $uploadOk = 0;
    }
    
    // Check file size
    if ($_FILES["fileInput"]["size"] > 500000) {
        echo "Sorry, your file is too large.";
        $uploadOk = 0;
    }
    
    // Allow certain file formats
    if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
    && $imageFileType != "gif" ) {
        echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
        $uploadOk = 0;
    }
    
    // Check if $uploadOk is set to 0 by an error
    if ($uploadOk == 0) {
        echo "Sorry, your file was not uploaded.";
    // if everything is ok, try to upload file
    } else {
        if (move_uploaded_file($_FILES["fileInput"]["tmp_name"], $targetFile)) {
            echo "The file ". basename( $_FILES["fileInput"]["name"]). " has been uploaded.";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }
}
?>
