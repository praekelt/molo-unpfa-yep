'use strict';

var gulp              =   require('gulp'),
    sass              =   require('gulp-sass'),
    watch             =   require('gulp-watch'),
    cleanCSSMinify    =   require('gulp-clean-css'),
    rename            =   require('gulp-rename'),
    gzip              =   require('gulp-gzip'),
    notify            =   require('gulp-notify'),
    sourcemaps        =   require('gulp-sourcemaps'),
    livereload        =   require('gulp-livereload');

var sassPaths = [
    'tuneme/client/css/opera_single_view.scss',
    'tuneme/client/css/style.scss',
    'tuneme/client/css/versions.scss',
    'tuneme/client/css/state_320/state_320.scss',
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
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSSMinify())
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

gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('tuneme/client/css/*.scss', ['styles']);
});

gulp.task('styles', ['styles:dev', 'styles:prd']);
gulp.task('default', ['styles']);
