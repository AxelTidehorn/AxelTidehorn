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
        <p>
            Mitt namn är Axel Tidehorn och jag är en Jönköpingsbaserad fotograf vars mål är att fånga och berätta Er historia. Oavsett om det är Ert företag, produkt, familj, husdjur eller Er stora dag.
            Era önskningar och mål är det viktigaste för mig och jag tror att vi tillsammans kan fånga ljuset och skapa något magiskt!
        </p>
        <div class="acc-wrapper">
            <button type="button" name="button" class="accordion">Porträtt</button>
            <div class="panel">
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </div>
            <button type="button" name="button" class="accordion">Analog</button>
            <div class="panel">
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </div>
            <button type="button" name="button" class="accordion"><Analog>Event</Analog></button>
            <div class="panel">
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </div>
        </div>
    </div>
    <script>
    var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}
</script>
</main>
<?php get_footer(); ?>
