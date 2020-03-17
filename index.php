
<?php get_header(); ?>


<div class="hero">
    <!-- div id="hero-bg" class="hero-background parallax hidden" data-depth="-0.2" style="background-image:url(<?php echo get_template_directory_uri(); ?>/img/hero-bg.jpg)"></div>
    <div class="hero-overlay"!-->
        <div class="hero-text">
            <!--h2 class="fade-text">AXEL TIDEHORN</h2!-->
            <p class="fade-text">
                Landskap • Event • Porträtt • Arkitektur
            </p>
        </div>

    </div>
    <div class="wave-wrapper-top">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#263f2c" fill-opacity="1" d="M0,160L1440,96L1440,0L0,0Z"></path></svg>
    </div>
</div>
<main>
    <?php
        if ( have_posts() ) {

        echo "<div class='grid hidden'>";

            while ( have_posts() ) {
                the_post();

    ?>
            <!--<div class="grid-sizer"></div>
            <div class="grid-item">
                <a href=<?php //echo the_permalink();?>>
                    <img src='<?php //echo get_the_post_thumbnail_url($post->ID,'full') ?>'>
                    <?php //the_title() ?>
                </a>
            </div>-->

            <div class="grid-sizer"></div>
            <div class="grid-item">
                <div class="grid-content-wrapper" onClick="openImageModal('<?php echo get_the_post_thumbnail_url($post->ID,'full') ?>','<?php the_title() ?>','<?php echo get_the_content() ?>')">
                    <img src='<?php echo get_the_post_thumbnail_url($post->ID,'full') ?>'>
                    <?php //the_title() ?>
                </div>
            </div>

    <?php


            } // end while

        echo "</div>";

        }

?>

<!-- Modal -->

<div class="modal" id="modal"  onClick="closeModal()">
    <!--<button onClick="closeModal()" class="close-modal">Close modal</button>-->
    <div class="modal-image" id="modal-image">

    </div>
    <div class="info">
        <div class="info-wrapper">
            <h3 id="title"></h3>
            <p id="content"></p>
        <div>
    </div>
</div>

<!-- Modal end -->
<script type="text/javascript" src="<?php bloginfo('template_url'); ?>/scripts/text-reveal.js"></script>
<script type="text/javascript" src="<?php bloginfo('template_url'); ?>/scripts/parallax.js"></script>
<script type="text/javascript" src="<?php echo get_template_directory_uri(); ?>/scripts/modal.js"></script>

<script type="text/javascript">

    const img = new Image();
    img.onload = function() {
        document.getElementById("hero-bg").classList.remove("hidden");
    };

    img.src = "<?php echo get_template_directory_uri(); ?>/img/hero-bg.jpg";

</script>

<script>
        // external js: masonry.pkgd.js, imagesloaded.pkgd.js

        // init Masonry
        var grid = document.querySelector('.grid');

        var msnry = new Masonry( grid, {
          itemSelector: '.grid-item',
          columnWidth: '.grid-sizer',
          percentPosition: true
        });

        imagesLoaded( grid ).on( 'progress', function() {
          // layout Masonry after each image loads
          msnry.layout();
        });


        window.addEventListener("load",()=>{
                console.log("loaded!")
                const hiddenItems = document.querySelectorAll(".hidden");

                for(let i = 0; i < hiddenItems.length; i++){
                    hiddenItems[i].classList.remove("hidden");
                    hiddenItems[i].classList.add("revealed");
                }
        });


   </script>
</main>
<div class="wave-wrapper">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="#263f2c" fill-opacity="1" d="M0,224L1440,64L1440,320L0,320Z"></path></svg>
</div>
<div class="contact-wrapper" id="contact">
    <p>
        Ska vi jobba tillsammans?
    </p>
    <div class="email-wrapper">
        <a href="mailto:kontakt@axeltidehorn.se">kontakt@axeltidehorn.se</a>
    </div>

</div>





<?php get_footer(); ?>
