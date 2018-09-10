var path = require('path'),
    gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    less = require('gulp-less'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    mediaqueries = require('gulp-group-css-media-queries'),
    cssnano = require('gulp-cssnano'),
    concat = require('gulp-concat'),
    sourcemaps = require('gulp-sourcemaps'),
    rename = require('gulp-rename'),
    check = require('gulp-if'),
    config = require('./config');


var css = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(check(!!args.concat, concat(args.concat + '.css')))
            .pipe(autoprefixer(config.autoprefixer).on('error', config.error))
            .pipe(mediaqueries().on('error', config.error))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, cssnano(config.cssnano).on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

css.less = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(less().on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.css')))
            .pipe(autoprefixer(config.autoprefixer).on('error', config.error))
            .pipe(mediaqueries().on('error', config.error))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, cssnano(config.cssnano).on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

css.sass = function (dest, param, args) {
    args = config.args(args, {
        min: true,
        sass: config.sass
    });
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(sass({includePaths: args.sass}).on('error', sass.logError))
            .pipe(check(!!args.concat, concat(args.concat + '.css')))
            .pipe(autoprefixer(config.autoprefixer).on('error', config.error))
            .pipe(mediaqueries())
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, cssnano(config.cssnano).on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};


module.exports = css;
