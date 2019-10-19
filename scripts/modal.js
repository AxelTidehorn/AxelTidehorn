const modal = document.getElementById("modal");
const image = document.getElementById("modal-image");

function openImageModal(img_url){
    image.style.backgroundImage  = `url(${img_url})`;
    image.style.backgroundSize  = `contain`;
    image.style.backgroundRepeat  = `no-repeat`;
    image.style.backgroundPosition  = `center`;
    modal.classList.add("visible");
}

function closeModal(){
    modal.classList.remove("visible");
}