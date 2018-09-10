var fs = require('fs'),
    path = require('path'),
    consolidate = require('gulp-consolidate'),
    gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    iconfont = require('gulp-iconfont'),
    iconfontCss = require('gulp-iconfont-css'),
    config = require('./config');


var icon = function (dest, param, args) {
    args = config.args(args);
    if (args.fontName) {
        config.iconfont.fontName = config.iconfontCss.fontName = args.fontName;
    }
    if (args.targetPath) {
        config.iconfontCss.targetPath = args.targetPath;
    }
    if (args.cssClass) {
        config.iconfontCss.cssClass = args.cssClass;
    }
    if (dest && param) {
        gulp.src(param)
            .pipe(plumber())
            .pipe(iconfontCss(config.iconfontCss).on('error', config.error))
            .pipe(
                iconfont(config.iconfont)
                    /*
                    .on('codepoints', function (codepoints) {
                        glyphs = _.map(codepoints, function (codepoint) {
                            return {
                                fileName: codepoint.name,
                                codePoint: codepoint.codepoint.toString(16).toUpperCase()
                            };
                        });
                        gulp.src(path.join(__dirname, 'iconfont.tpl'))
                            .pipe(consolidate('lodash', {
                                glyphs: glyphs,
                                cssClass: 'icon'
                            }))
                            .pipe(gulp.dest(path.join(dest, 'fonts', config.iconfont.fontName, '_icons.scss')));
                    })
                    */
                    .on('error', config.error)
            )
            .pipe(gulp.dest(path.join(dest, 'fonts', config.iconfont.fontName)));
    }
};


icon.read = function (dest, param, args) {
    args = config.args(args);
    if (dest && param) {
        fs.readdir(param, function (err, files) {
            if (!err) {
                icon(
                    dest,
                    files
                        .filter(function (file) {
                            return file.match(/^.+\.svg/i);
                        })
                        .map(function (file) {
                            return path.join(param, file);
                        }),
                    args
                );
            }
        });
    }
};


icon.reads = function (dest, param, args) {
    args = config.args(args);
    if (dest && param) {
        if (typeof param == 'string') {
            param = [param];
        }
        var svgs = [],
            fn = function (idx) {
                idx = idx || 0;
                if (idx < param.length) {
                    fs.readdir(param[idx], function (err, files) {
                        if (!err) {
                            files
                                .filter(function (file) {
                                    return file.match(/^.+\.svg/i);
                                })
                                .forEach(function (file) {
                                    svgs.push(path.join(param[idx], file));
                                });
                        }
                        fn(++idx);
                    });
                } else {
                    if (svgs) {
                        icon(dest, svgs, args);
                    }
                }
            };
        fn();
    }
};


module.exports = icon;
