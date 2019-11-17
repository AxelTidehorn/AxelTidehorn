<?php /* Template Name: About-template */ ?>
<?php get_header(); ?>
<main>
    <div class="about-wrapper">
        <h2>Axel Tidehorn</h2>
        <p>

        </p>
        <p>
            Ordet fotografi kommer från grekiskans phōs och graphé som översätts till ljus och skriva. Och om man lägger till tid så är det exakt det jag som fotograf gör. Skriver, berättar, genom att fånga ljus och tid i ögonblick.
        </p>
        <div class="portrait-wrapper">
            <div class="portrait"style="background-image:url(<?php echo get_template_directory_uri();?>/img/hero-bg5.jpg)">
                <div class="portrait-overlay">
                </div>

            </div>
        </div>
        <p>
            Mitt namn är Axel Tidehorn och jag är en Jönköpingsbaserad fotograf vars mål är att fånga och berätta Er historia. Oavsett om det är Ert företag, produkt, familj, husdjur eller Er stora dag.
            Era önskningar och mål är det viktigaste för mig och jag tror att vi tillsammans kan fånga ljuset och skapa något magiskt!
        </p>
        <div class="acc-wrapper">
            <button type="button" name="button" class="accordion">Porträtt</button>
            <div class="panel">
                <p>
                    Ett bra porträtt öppnar nya dörrar oavsett om det
                </p>
            </div>
            <button type="button" name="button" class="accordion">Analog</button>
            <div class="panel">
                <p>
                    Vissa ögonblick är så unika att det bara måste fångas på ett lika unikt sätt, på 35mm film.
                    Ett äkta hantverk där varje bild räknas och måste vara perfekt. Analoga bilder har en känsla som man kan försöka efterlikna men aldrig riktigt fånga.
                    Kontrastfyllda svartvita bilder, underbara färger och subtilt gryn får Er att sticka ut från mängden. Oavsett om det är till ett event, produkter eller porträtt.
                    <br>
                    <br>
                    I och med processen om film innebär så är det lite dyrare och tar lite längre tid men jag kan garantera att det är värt det för det som är viktigast för Er.
                </p>
        </div>
    </div>
    <script>
        const accordions = document.getElementsByClassName("accordion");
        var i;

        for (i = 0; i < accordions.length; i++) {
            accordions[i].addEventListener("click", function(){
                expandAccordion(this);
            });
        }

        function expandAccordion(elt){

            const activeElt = document.querySelector(".active");

            if(activeElt){//Check if exists
               if(activeElt !== elt){
                    activeElt.classList.remove("active");
                    activeElt.nextElementSibling.style.maxHeight = null;
               }
            }

            elt.classList.toggle("active");
            var panel = elt.nextElementSibling;
            if (panel.style.maxHeight) {
                panel.style.maxHeight = null;
            } else {
                panel.style.maxHeight = panel.scrollHeight + "px";
            }
        }

</script>
</main>
<?php get_footer(); ?>
