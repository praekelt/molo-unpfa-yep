const path = require('path'),
      gulp = require('gulp'),
      sass = require('gulp-sass'),
      watch = require('gulp-watch'),
      cleanCSSMinify = require('gulp-clean-css'),
      rename = require('gulp-rename'),
      gzip = require('gulp-gzip'),
      notify = require('gulp-notify'),
      sourcemaps = require('gulp-sourcemaps'),
      livereload = require('gulp-livereload'),
      rev = require('gulp-rev')
      _ = require('lodash');


const paths = {
  base: 'tuneme/static',
  styles: {
    src: [
      'tuneme/styles/opera_single_view.scss',
      'tuneme/styles/style.scss',
      'tuneme/styles/state_320/state_320.scss',
    ],
    dest: 'tuneme/static/new/css'
  }
};


function styles(env, s) {
  return s
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSSMinify());
}


function serializeManifest(dir) {
  return manifest => _(manifest)
    .mapKeys((_, filename) => path.join('new', dir, filename))
    .mapValues(filename => path.join('new', dir, filename))
    .thru(res => JSON.stringify(res, null, 2))
    .value();
}


gulp.task('styles:prd', () => {
  return styles('prd', gulp.src(paths.styles.src))
    .pipe(rev())
    .pipe(gulp.dest(paths.styles.dest))
    .pipe(rev.manifest({
      transformer: {
        parse: JSON.parse,
        stringify: serializeManifest('css')
      }
    }))
    .pipe(gulp.dest(paths.base));
});

gulp.task('styles:dev', () => {
  const s = gulp.src(paths.styles.src)
    .pipe(sourcemaps.init());

  return styles('dev', s)
    .pipe(sourcemaps.write('../maps'))
    .pipe(gulp.dest(paths.styles.dest));
});

gulp.task('watch', () => {
  livereload.listen();
  gulp.watch('iogt/styles/*.scss', ['styles']);
});

gulp.task('styles', ['styles:dev', 'styles:prd']);
gulp.task('default', ['styles']);
