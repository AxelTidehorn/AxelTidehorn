    <?php get_header(); ?>



<main>

    <?php
        if ( have_posts() ) {
            while ( have_posts() ) {
                the_post();



    ?>
            <?php the_post_thumbnail()?>

            <p><?php the_content() ?>


    <?php


            } // end while
        }


?>

</main>



<?php get_footer(); ?>
