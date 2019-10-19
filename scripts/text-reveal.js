const textElts = document.querySelectorAll(".fade-text");
const texts = [];

for(let i = 0; i < textElts.length; i++){
    texts.push(textElts[i].innerHTML);
    textElts[i].innerText = "";
}

for(let i = 0; i < texts.length; i++){

    for(let j = 0; j < texts[i].length; j++){
        const elt = document.createElement("span");
        elt.classList.add("char");
        elt.innerText = texts[i][j];
        textElts[i].appendChild(elt);
    }

}



{

    for(let i = 0; i < textElts.length; i++){
        const chars = textElts[i].querySelectorAll(".char");

        const revealChars = async() =>{

            for(let i = 0; i < chars.length; i++){
                (function(ind) {
                    setTimeout(function(){chars[ind].classList.add("reveal");;}, 500 + (50 * ind));
                })(i);
            }

        }

        revealChars();

    }


}