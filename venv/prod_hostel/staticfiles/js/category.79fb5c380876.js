const castes=document.querySelector(".cast")
const noncreamylayerblock=document.querySelector(".Non-creamy-layer-block");
const casteblock=document.querySelector(".caste-file-block");
const domicile=document.querySelector(".domicile-block");


castes.addEventListener('change',(event)=>{
    let selectedcaste=event.target.value;
    console.log(selectedcaste)


    if(selectedcaste==='SC'){
        noncreamylayerblock.style.display="none";
        console.log("SC");
    }
    else if(selectedcaste==="OPEN" ){
        noncreamylayerblock.style.display="none";
        domicileblock.style.display="none";
    }
})

