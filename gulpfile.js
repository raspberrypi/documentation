const gulp = require('gulp')
const clean = require('gulp-clean')
const concat = require('gulp-concat')
var merge = require('merge-stream');
const sass = require('gulp-sass')
const serve = require('gulp-serve')
const shell = require('gulp-shell')
const uglify = require('gulp-uglify-es').default

const { buildSrc, buildTmp, buildDest } = require('./paths')

gulp.task('setup', function() {
  return gulp
    .src('*.*', {
      read: false,
    })
    .pipe(gulp.dest(`./${buildDest}`))
    .pipe(gulp.dest(`./${buildTmp}`))
})

gulp.task('clean', function() {
  let tmpDir = gulp.src(buildDest, {read: false })
    .pipe(clean());

  let buildDir = gulp.src(buildTmp, {read: false })
    .pipe(clean());

  return merge(tmpDir, buildDir);
})

gulp.task(
  'serve',
  serve({
    root: [`${buildDest}`],
    port: 8000,
  })
)

gulp.task('generate', shell.task('eleventy --passthroughall'))

gulp.task('watch', function() {
  gulp.watch([
    buildSrc + '/**/*',
    '!' + buildSrc + '/_site/**/*'
  ], gulp.parallel('build'))
})

gulp.task(
  'build',
  gulp.series('setup', 'clean')
)
