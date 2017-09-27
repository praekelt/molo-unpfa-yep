'use strict';

var gulp              =   require('gulp'),
    sass              =   require('gulp-sass'),
    sassLint          =   require('gulp-sass-lint'),
    sassGlob          =   require('gulp-sass-glob'),
    cleanCSSMinify    =   require('gulp-clean-css'),
    watch             =   require('gulp-watch'),
    rename            =   require('gulp-rename'),
    gzip              =   require('gulp-gzip'),
    notify            =   require('gulp-notify'),
    sourcemaps        =   require('gulp-sourcemaps'),
    livereload        =   require('gulp-livereload'),
    browserSync       =   require('browser-sync').create(),
    reload            =   browserSync.reload;

var templatesPath = 'tuneme/templates/new';
var sassPaths = [
    'tuneme/styles/tuneme/style-320.s+(a|c)ss',
    'tuneme/styles/tuneme/style-opera.s+(a|c)ss',
    'tuneme/styles/tuneme/style-rtl.s+(a|c)ss',
    'tuneme/styles/tuneme/style.s+(a|c)ss',
];

var sassDest = {
     prd: 'tuneme/static/new/css/prd',
     dev: 'tuneme/static/new/css/dev'
};

function styles(env) {
  var s = gulp.src(sassPaths);
  var isDev = env === 'dev';
  if (isDev) s = s
    .pipe(sourcemaps.init());
    s = s
    .pipe(sassGlob())
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSSMinify())
    //.pipe(sassLint())
    //.pipe(sassLint.format())
    //.pipe(sassLint.failOnError());
    if (isDev) s = s
        .pipe(sourcemaps.write('/maps'));
        return s
        .pipe(gulp.dest(sassDest[env]))
        .pipe(notify({ message: `Styles task complete: ${env}` }));
}

gulp.task('styles:prd', function() {
  return styles('prd');
});
gulp.task('styles:dev', function() {
  return styles('dev');
});

gulp.task('serve', function() {
    browserSync.init({
        'proxy': 'localhost:8000/'
    });
    gulp.watch(sassPaths + '/**/*.scss', ['styles:dev', 'styles:prd']);
    gulp.watch(templatesPath + '/**/*.html').on('change', reload);
});

gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('tuneme/styles/tuneme/**/**.scss', ['styles']);
});

gulp.task('styles', ['styles:dev', 'styles:prd']);
gulp.task('default', ['styles']);
