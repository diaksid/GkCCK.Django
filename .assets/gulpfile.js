var path = require('path'),
    gulp = require('gulp'),
    src = __dirname,
    inc = path.join(__dirname, 'vendor'),
    dest = path.normalize(path.join(__dirname, '..', 'web', 'assets'));

var css = require(path.join(__dirname, 'utils', 'css')),
    js = require(path.join(__dirname, 'utils', 'js')),
    icon = require(path.join(__dirname, 'utils', 'icon'));

// ----------

gulp.task('style:app', function () {
    css.sass(path.join(dest, 'css'), [
        path.join(src, 'stylesheets', 'app.scss'),
        path.join(src, 'stylesheets', 'error.scss'),
        path.join(src, 'stylesheets', 'admin.scss')
    ]);
});


gulp.task('style:proj', function () {
    css.sass(path.join(dest, 'css'), [
        path.join(inc, 'stylesheets', 'proj', 'proj.scss')
    ]);
});


gulp.task('style:bootstrap', function () {
    css.sass(path.join(dest, 'css'), [
        path.join(inc, 'stylesheets', 'bootstrap', 'bootstrap.scss')
    ]);
});


gulp.task('style:vendor', function () {
    css.sass(path.join(dest, 'css'), [
        path.join(inc, 'stylesheets', 'animate', 'animate.scss')
    ], {
        concat: 'vendor'
    });

    css.sass(path.join(dest, 'css'), [
        path.join(inc, 'stylesheets', 'imperavi', 'redactor.scss'),
        path.join(inc, 'stylesheets', 'imperavi', 'clips.scss')
    ], {
        concat: 'redactor'
    });
});

// ----------

gulp.task('script:app', function () {
    js.coffee(path.join(dest, 'js'), [
        path.join(src, 'javascripts', 'app.coffee'),
    ]);
});


gulp.task('script:proj', function () {
    js.coffee(path.join(dest, 'js'), [
        path.join(inc, 'javascripts', 'proj', 'proj.coffee'),
        path.join(inc, 'javascripts', 'proj', '_animation.coffee'),
        path.join(inc, 'javascripts', 'proj', '_helpers.coffee'),
        path.join(inc, 'javascripts', 'proj', '_lazyload.coffee'),
        path.join(inc, 'javascripts', 'proj', '_lightbox.coffee'),
        path.join(inc, 'javascripts', 'proj', '_extend.coffee'),
        path.join(inc, 'javascripts', 'proj', 'wrapper', '_yandex.coffee')
    ], {
        concat: 'proj'
    });

    js.coffee(path.join(dest, 'js'), [
        path.join(inc, 'javascripts', 'proj', 'canvas', 'grid.coffee'),
        path.join(inc, 'javascripts', 'proj', 'canvas', 'snow.coffee')
    ], {
        dirname: 'canvas'
    });
});


gulp.task('script:bootstrap', function () {
    js(path.join(dest, 'js'), [
        path.join(inc, 'javascripts', 'bootstrap', 'util.js'),
        path.join(inc, 'javascripts', 'bootstrap', 'alert.js'),
        path.join(inc, 'javascripts', 'bootstrap', 'button.js'),
        path.join(inc, 'javascripts', 'bootstrap', 'collapse.js'),
        path.join(inc, 'javascripts', 'bootstrap', 'dropdown.js'),
        path.join(inc, 'javascripts', 'bootstrap', 'tab.js')
    ], {
        concat: 'bootstrap'
    });
});


gulp.task('script:vendor', function () {
    js(path.join(dest, 'js'), [
        path.join(inc, 'javascripts', 'wow.js'),

        path.join(inc, 'javascripts', 'jquery', 'easing.js'),
        path.join(inc, 'javascripts', 'jquery', 'cookie.js'),
        path.join(inc, 'javascripts', 'jquery', 'bgswitcher.js')

    ], {
        concat: 'vendor'
    });

    js(path.join(dest, 'js'), [
        path.join(inc, 'javascripts', 'imperavi', 'redactor.js'),
        path.join(inc, 'javascripts', 'imperavi', 'plugins', 'fullscreen', 'fullscreen.js'),
        path.join(inc, 'javascripts', 'imperavi', 'langs', 'ru.js')
    ], {
        concat: 'redactor'
    });

    js(path.join(dest, 'js', 'lib'), [
        path.join(inc, 'javascripts', 'html5', 'es5-shim.js'),
        path.join(inc, 'javascripts', 'html5', 'html5shiv.js'),
        path.join(inc, 'javascripts', 'html5', 'html5shiv-printshiv.js'),
        path.join(inc, 'javascripts', 'html5', 'respond.js')
    ], {
        concat: 'html5bility'
    });

    js.ify(path.join(dest, 'js', 'lib'), [
        path.join(inc, 'javascripts', 'flex', 'index.js'),
    ], {
        basename: 'flexibility'
    });
});

// ----------

gulp.task('font:icons', function () {
    icon.read(dest, path.join(src, 'icons'));
});

// ----------

gulp.task('watch', function () {
    gulp.watch([
        path.join(src, 'icons', '**')
    ], [
        'font:icons'
    ]);
});

// ----------

gulp.task('default', [
    'style:app',
    'style:proj',
    'style:bootstrap',
    'style:vendor',

    'script:app',
    'script:proj',
    'script:bootstrap',
    'script:vendor'
]);
