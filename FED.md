#### FED workflow
  You maintain or add frontend UI features.
  Conduct browser performance tests and updates.
  Create accessible websites which means mobile or feature phone first media question.
  Readable HTML and Django template HTML
  Cascading SASS

#### HTML Template Approach
  We use SMACSS, BEM methodologies

#### BEM
  [Introduction to BEM](https://en.bem.info/methodology/quick-start/)
  [BEM](http://getbem.com/introduction/)

#### BEM Naming Convention
    Languages
    Language__current
    Language__title
    Language__title--icon
    Language__dropdown-button

    Language__list
    Language-list__toggle
    Language-list__item

### e.g. Languages block
  ```
    <div class="languages">
      <h2 class="language__title">Language block</h2>
      <ul class="language-list">
        <li class="language-list__item">
          <a href="#" class="language-list__anchor">English</a>
        </li>
        <li class="language-list__item">
          <a href="#" class="language-list__anchor">Xhosa</a>
        </li>
      </ul>
    </div>
  ```


### CSS Styles Approach
    We write CSS styles using SCSS extension for rich CSS features.
    [Sass](  https://sass-lang.com/)

    SCSS is compiled using [gulp.js](https://gulpjs.com/) tast runner workflow and or [Webpack](webpack.js) bundler workflow.

    We use SMACSS methodologies / CSS structure and naming convention.
    [SMACCS Cookbook](  https://smacss.com/book/)

    Application CSS Folder:
    ```
      /static/css/sass/app-name/
        /layout/
          _l-header.scss
          _l-footer.scss
        /modules
          _m-article-list.scss
          _m-article.scss
        /state
          _s-article-list.scss
          _s-article.scss
        /utils
          variables.scss
          color.scss
        _base.scss
        _versions.scss
        styles-rtl.scss
    ```

#### SMACSS
  * variables / colors.scss
    * $de_york - #2A9B58;
    * $robin_egg_blue - #37BFBE;
    * $mandy - #EC3B3A;
    * $danube - #5F7AC9;
    * $roman - #EF9955;
    * $saffron - #F2B438;
    * $medium_violet - #B62A99;

#### FILE PATH: /styles/app-name/
    * /layout
      * _l-header.scss
      * _l-footer.scss
      * _l-layout.scss | @import all layout compoments
    * /modules
      * _m-article-list.scss
      * _m-article.scss
      * _m-modules.scss | @import all modules compoments
    * /state
      * _s-article-list.scss
      * _s-article.scss
      * _s-state.scss | @import all state compoments
    * /variables
      * variables.scss
      * color.scss
    * _base.scss
    * _versions.scss
    * styles.scss | @import all compoments
    * styles-rtl.scss

#### OUTPUT FILE PATH:
    * /static/css/dev with sourcemaps /maps
      * /static/css/prd

#### CSS / BEM Linting
  https://github.com/postcss/postcss-bem-linter
  * - Enforce coding standard rules


#### COMPRESSION / AUTOMATION
  Requirements:
  Must have node.js npm and gulp installed globally

  * - npm install gulp-cli -g

  For asset bundling & processing, concatenating and minification file scripts:
  * - gulpfile.js
  * - package.json

#### On your Command Line run the following commands on the app:
  * - npm install [Node](https://nodejs.org/en/)
  * - gulp [Node](https://nodejs.org/en/)

#### IMAGES FORMATS:
    * SVG, PNG, Sprites icons
    * Images must be compressed
