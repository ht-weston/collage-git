var gulp = require('gulp'),
    rename = require('gulp-rename'),
    zip = require('gulp-zip'),
    del = require('del'),
    moment = require('moment'),
    exec = require('child_process').exec;
    plumber = require('gulp-plumber');

var src = './src/**/*.tex'
var draft ='./dist/draft'
var pub ='./dist/publish'

gulp.task('clean',() => {
    return del('./dist/draft');
});

gulp.task('compile', function(cb) {
    exec('latexmk -outdir=../dist/draft -pdf -cd src/*.tex', function(err,stdout,stderr) {
        console.log(stdout);
        console.log(stderr);
        cb(err);
    });
})

gulp.task('default', gulp.series('compile'));

gulp.task('archive', gulp.series('default',function () {
    // single instance compile and open Okular.
    return gulp
        .src(['./dist/draft/*.pdf'])
        .pipe(rename({
            prefix:"HansTremmel_"
        }))
        .pipe(zip(moment().format('YYYYMMDD') + '_proposal_pkg.zip'))
        .pipe(gulp.dest('./dist/publish'));
}));

gulp.task('publish', gulp.series('default',function () {
    // single instance compile and open Okular.
    return gulp
        .src(['./dist/draft/*.pdf'])
        .pipe(rename({
            prefix:moment().format('YYYYMMDD') + "_HansTremmel_",
        }))
        .pipe(gulp.dest('./dist/publish'));
}));

gulp.task('view',function () {
    // compile view, create pkg/*.tex, zip with date.  Put pdf in foremost 
    return exec('okular ./dist/draft/*.pdf &');
});

gulp.task('watch', gulp.series('default', 'view', function () {
    // Open a gulp watcher, okular, and type away to view changes.
    gulp.watch(['./src/**/*'],gulp.series('default'));

}));

