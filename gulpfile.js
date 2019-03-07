const gulp = require('gulp')
const clean = require('gulp-clean')
const concat = require('gulp-concat')
const merge = require('merge-stream');
const rename = require('gulp-rename');
const sass = require('gulp-sass')
const serve = require('gulp-serve')
const shell = require('gulp-shell')
const uglify = require('gulp-uglify-es').default

const { buildSrc, buildTmp, buildDest } = require('./paths')

gulp.task('setup', function() {
  return gulp
    .src('*.*', {read: false})
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

gulp.task('copy', function() {
  return gulp
    .src([
      buildSrc + '/**/*',
      buildSrc + '/**/.*',
      '!node_modules/**'
    ])
    .pipe(gulp.dest(buildTmp));
})

gulp.task('renameReadme', function() {
  return gulp.src(buildTmp + '/**/README.md')
    .pipe(rename(function (path) {
      path.basename = "index";
    }))
    .pipe(gulp.dest(buildTmp));
})

gulp.task('deleteReadme', function() {
  return gulp.src(buildTmp + '/**/README.md')
    .pipe(clean({force: true}))
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
    '!{'+buildDest+','+buildDest+'/**}',
    '!{'+buildTmp+','+buildTmp+'/**}'
  ], gulp.parallel('build'))
})

gulp.task(
  'prep',
  gulp.series('clean', 'copy', 'renameReadme', 'deleteReadme')
)

gulp.task(
  'build',
  gulp.series('setup', 'prep', 'generate')
)
