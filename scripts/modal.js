const modal = document.getElementById("modal");
const image = document.getElementById("modal-image");

const titleElt = document.getElementById("title");
const contentElt = document.getElementById("content")

function openImageModal(img_url,title,content){

    titleElt.innerHTML = title;
    contentElt.innerHTML = content;

    image.style.backgroundImage  = `url(${img_url})`;
    image.style.backgroundSize  = `contain`;
    image.style.backgroundRepeat  = `no-repeat`;
    image.style.backgroundPosition  = `center`;
    modal.classList.add("visible");
}

function closeModal(){
    modal.classList.remove("visible");
}