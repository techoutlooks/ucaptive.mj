'use strict';

var gulp = require('gulp');
var ngAnnotate = require('gulp-ng-annotate');
var sourcemaps = require('gulp-sourcemaps');
var buffer = require('gulp-buffer');
var uglify = require('gulp-uglify');
var tap = require('gulp-tap');
var browserify = require('browserify');
var babel = require('babelify');
var rename = require('gulp-rename');
var livereload = require('gulp-livereload');
var spawn = require('child_process').spawn;
var argv = require('yargs')
  .default('port', 8000)
  .default('address', 'localhost')
  .argv;

// var gutil = require('gulp-util');
// var watchify = require('watchify');


// Concatenate, Browserify & Minify JS
gulp.task('build', () => {

  return gulp.src([
      './ucaptive/static/js/app.js',
  ], { read: false })
    .pipe(tap((file) => {
      file.contents = browserify(file.path, {
        debug: true,
        paths: [
            './ucaptive/static/js/',
            './apps/layout/static/js/',
            './apps/accounts/static/js/',
            './apps/djra/radmin/static/js/',
            './components/bower_components/',
            './components/vendor/',
        ]
      }).transform(babel, {
        presets: [ 'es2015' ]
      }).bundle();
    }))

    .pipe(ngAnnotate())
    .pipe(buffer())
    .pipe(sourcemaps.init({ loadMaps: true }))
    .pipe(rename('app.min.js'))
    // .pipe(uglify())
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./staticfiles/js/'));
    
});

// 
gulp.task('watch', function () {
  gulp.watch([
      './ucaptive/static/js/**/*.js',
      './apps/**/*.js'
      ], ['build']
  );
});

// // Default Task starts our development workflow
function start_dev_server(done) {
  livereload.listen();

  console.log("Starting Django runserver http://"+argv.address+":"+argv.port+"/");
  var args = ["manage.py", "runserver", argv.address+":"+argv.port];
  var python = process.env['VIRTUAL_ENV'] + '/bin/python';
  // var python = '/home/ceduth/.envs/ucaptive.cloud.com.gn/bin/python';

  var runserver = spawn(python, args, {
    stdio: "inherit",
  });
  runserver.on('close', function(code) {
    if (code !== 0) {
      console.error('Django runserver exited with error code: ' + code);
    } else {
      console.log('Django runserver exited normally.');
    }
  });
  done();
}
gulp.task('start_dev_server', ['build'], start_dev_server)


// Starts our development workflow
gulp.task('default', ['start_dev_server', 'build', 'watch'], function (done) {
  livereload.listen();
  done();
});
