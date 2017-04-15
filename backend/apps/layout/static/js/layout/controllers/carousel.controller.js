/**
 * Created by ceduth on 3/2/17.
 * layout
 * @namespace app.layout.controllers
 */


/**
 * @name carousel
 * @desc ui-bootstrap Carousel Controller
 */
class CarouselCtrl {
    constructor() {

        // template vars
        this.myInterval = 5000;
        this.noWrapSlides = false;
        this.active = 0;

        let slides = this.slides = [];
        let currIndex = 0;


        this.addSlide = () => {
            let newWidth = 1920 + slides.length + 1;
            slides.push({
                image: '//unsplash.it/' + newWidth + '/627',
                text: ['Test image', 'Test photo', 'That is so cool', 'I love that'][slides.length % 4],
                id: currIndex++
            });
        };


        for (let i = 0; i < 4; i++) {
            this.addSlide();
        }
    }

}

export default  CarouselCtrl;

