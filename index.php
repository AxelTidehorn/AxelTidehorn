<?php get_header(); ?>

<!---->

<main>




    <?php
        if ( have_posts() ) {

        echo "<div class='grid hidden'>";

            while ( have_posts() ) {
                the_post();

    ?>
            <div class="grid-sizer"></div>
            <div class="grid-item">
                <a href=<?php echo the_permalink();?>>
                    <img src='<?php echo get_the_post_thumbnail_url($post->ID,'full') ?>'>
                    <!--figure style="background:url('<?php //echo get_the_post_thumbnail_url($post->ID,'full') ?>'); background-size:cover; background-position:center;">
                    </figure-->
                    <!--
        <h2>
                        <?php the_title() ?>
                    </h2>-->
                </a>
            </div>
    <?php


            } // end while

        echo "</div>";

        }


?>

<div class="contact-wrapper" id="contact<">
    <p>
        Låt oss fånga ljuset tillsammans!
    </p>
    <a href="hej@axeltidehorn.se">hej@axeltidehorn.se</a>
</div>
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



<?php get_footer(); ?>
