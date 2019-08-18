<?php get_header(); ?>

<div class="hero-background">
<div class="hero-wrapper">
    <div class="left-wrapper">
        <img src="http://localhost/AxelTidehorn/wordpress/wp-content/uploads/2019/08/ProfBW2.png" alt="">
    </div>
    <div class="right-wrapper">
            <h1>Axel Tidehorn - Fotograf</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
    </div>
</div>
</div>

<main>




    <?php
        if ( have_posts() ) {

        echo "<ul class='grid'>";

            while ( have_posts() ) {
                the_post();

    ?>
            <li class="grid-item">
                <a href=<?php echo the_permalink();?>>
                    <figure style="background:url('<?php echo get_the_post_thumbnail_url($post->ID,'full') ?>'); background-size:cover; background-position:center;">
                    </figure>
                    <!--
        <h2>
                        <?php the_title() ?>
                    </h2>-->
                </a>
            </li>
    <?php


            } // end while

        echo "</ul>";

        }


?>

<div class="contact-wrapper" id="contact">
    <p>
        Låt oss fånga ljuset tillsammans!
    </p>
    <a href="hej@axeltidehorn.se">hej@axeltidehorn.se</a>
</div>

</main>



<?php get_footer(); ?>
