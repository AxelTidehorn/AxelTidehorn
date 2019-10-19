const parallaxElements = document.querySelectorAll(".parallax");

window.addEventListener("scroll",changeParallax);

const initialValue = 0;


function changeParallax(){

    const windowOffset = window.pageYOffset;

    for(let i = 0; i < parallaxElements.length; i++){

      const depth = parallaxElements[i].getAttribute("data-depth");
      const movement = (((windowOffset) * depth) + initialValue);
      const translate3d = " translate3d(0,"+ movement +"px,0)";

      parallaxElements[i].style['-webkit-transform'] = translate3d;
      parallaxElements[i].style['-moz-transform'] = translate3d;
      parallaxElements[i].style['-ms-transform'] = translate3d;
      parallaxElements[i].style['-o-transform'] = translate3d;
      parallaxElements[i].style.transform = translate3d;
    }

}