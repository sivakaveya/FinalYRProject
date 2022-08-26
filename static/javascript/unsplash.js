
  document.addEventListener("DOMContentLoaded", () => {
      apiRequest();
  });
  
  apiRequest = () => {
  
    value=[];
    const url = 'https://api.unsplash.com/search/photos?query='+input.value+'&per_page=30&client_id=SouHY7Uul-OxoMl3LL3c0NkxUtjIrKwf3tsGk1JaiVo';
  
    fetch(url)
  
    .then(response => {
      if (!response.ok) throw Error(response.statusText);
        return response.json();
     })
  
     .then(data => {
        loadImages(data);
     })
  
     .catch(error => console.log(error));   
  }
  
  loadImages = (data) => {
    // for(let i = 0;i < data.results.length;i++){
    //   let image = document.createElement("div");
    //   image.className = "img";
    //   image.style.backgroundImage = "url("+data.results[i].urls.raw + "&w=1366&h=768" +")";
    //   image.addEventListener("click", function(){
    //     console.log(1);
    //     $.getJSON($SCRIPT_ROOT+'/getimage',{
    //       image:$(this).css("background-image")
    //     },function(data){
    //       console.log(2)
    //       console.log(data.data);
    //     })
    //   });
    //   document.querySelector("#grid").appendChild(image);
    // }

  }
  
  