var path = require('path'),
    gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    coffee = require('gulp-coffee'),
    cjsx = require('gulp-cjsx'),
    babel = require('gulp-babel'),
    browserify = require('gulp-browserify'),
    rollup = require('gulp-rollup'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    rename = require('gulp-rename'),
    check = require('gulp-if'),
    argv = require('yargs').argv,
    config = require('./config');


var js = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.coffee = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(coffee(config.coffee).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(babel(config.babel.es6).on('error', config.error))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.ify = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        config.ify.debug = !argv.production;
        gulp.src(param, {read: false})
            .pipe(plumber())
            .pipe(browserify(config.ify).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(rename({extname: '.js'}))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.es6 = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(babel(config.babel.es6).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.react = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(babel(config.babel.react).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.rollup = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        let options = config.args(config.rollup, {
            input: param,
            external: args.external || [],
            globals: args.globals || {}
        });
        gulp.src(param)
            .pipe(plumber())
            .pipe(rollup(options).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.cjsx = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(cjsx(config.cjsx).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};

js.cjsxify = function (dest, param, args) {
    args = config.args(args, {min: true});
    if (dest && param) {
        config.cjsxify.debug = !argv.production;
        gulp.src(param, {read: false})
            .pipe(plumber())
            .pipe(browserify(config.cjsxify).on('error', config.error))
            .pipe(check(!!args.concat, concat(args.concat + '.js')))
            .pipe(check(!!args.dirname, rename({dirname: args.dirname})))
            .pipe(check(!!args.basename, rename({basename: args.basename})))
            .pipe(rename({extname: '.js'}))
            .pipe(gulp.dest(dest))
            .pipe(check(!!args.min, uglify().on('error', config.error)))
            .pipe(check(!!args.min, rename({suffix: '.min'})))
            .pipe(check(!!args.min, gulp.dest(dest)));
    }
};


module.exports = js;
