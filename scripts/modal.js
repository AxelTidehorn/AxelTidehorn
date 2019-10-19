console.log("modal!")

const modal = document.getElementById("modal");
const image = document.getElementById("modal-image");

function openImageModal(img_url){
    console.log(img_url)
    image.style.backgroundImage  = `url(${img_url})`;
    image.style.backgroundSize  = `contain`;
    image.style.backgroundRepeat  = `no-repeat`;
    image.style.backgroundPosition  = `center`;
    modal.classList.add("visible");
}

function closeModal(){
    console.log("closing")
    modal.classList.remove("visible");
}