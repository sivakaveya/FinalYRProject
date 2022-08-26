
ip=document.querySelector("#money");
slider=document.querySelector("#slider");
slider.addEventListener('input', function(){
    //console.log(1);
    ip.value=slider.value;
    //console.log(3);
},false);

ip.addEventListener('input',function(){
    //console.log(ip.value);
    if(ip.value==""){
        slider.value=0;
    }
    slider.value=ip.value;
    if(ip.value==""){
        slider.value=0;
    }
    //console.log(slider.value);
    //console.log(ip.value);
},false);