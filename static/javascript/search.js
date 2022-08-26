function previewFile(input){
    var file = $("#text").get(0).files[0];

    if(file){
        var reader = new FileReader();

        reader.onload = function(){
            $("#img-change").css({"background-image": "url("+reader.result+")"}); 
        }

        reader.readAsDataURL(file);
    }
}