var path = require('path'),
    util = require('gulp-util'),
    rollup = {
        babel: require('rollup-plugin-babel'),
        resolve: require('rollup-plugin-node-resolve')
    };

var root = path.dirname(__dirname);


module.exports = {
    sourceMaps: {
        addComment: false,
        includeContent: false
    },

    sass: [
        path.join(root, 'stylesheets'),
        path.join(root, 'vendor', 'stylesheets')
    ],

    cssnano: {
        discardComments: {
            removeAll: true
        },
        zindex: false
    },

    autoprefixer: {
        browsers: [
            'Android 2.3',
            'Android >= 4',
            'Chrome >= 20',
            'Firefox >= 24',
            'Explorer >= 8',
            'iOS >= 6',
            'Opera >= 12',
            'Safari >= 6'
        ],
        cascade: true
    },

    coffee: {
        bare: true
    },

    ify: {
        insertGlobals: false,
        ignoreMissing: true
    },

    babel: {
        es6: {
            presets: [
                'env',
                'stage-0'
            ]
        },
        react: {
            presets: [
                'react'
            ]
        }
    },

    rollup: {
        name: 'main.js',
        format: 'umd',
        plugins: [
            rollup.babel({
                presets: [
                    ['env', {modules: false}]
                ],
                plugins: [
                    'external-helpers'
                ]
            })
        ]
    },

    cjsx: {
        bare: true
    },

    cjsxify: {
        extensions: [
            '.cjsx',
            '.coffee'
        ],
        transform: [
            'coffee-reactify'
        ],
        insertGlobals: false
    },

    eslint: {
        rules: {
            'new-cap': 0,
            'no-underscore-dangle': 0,
            'no-console': 0,
            'no-alert': 1
        },
        globals: {
            'ProJ': true,
            'Modernizr': true,
            'ymaps': true
        },
        envs: [
            'browser'
        ]
    },

    iconfont: {
        fontName: 'iconfont',
        prependUnicode: false,
        appendCodepoints: true,
        normalize: true,
        formats: [
            'eot',
            'woff',
            'woff2',
            'ttf',
            'svg'
        ],
        timestamp: Math.round(Date.now() / 1000)
    },

    iconfontCss: {
        fontName: 'iconfont',
        fontPath: '.',
        path: path.join(__dirname, 'iconfont.tpl'),
        targetPath: '_icons.scss',
        cssClass: 'icon'
    },

    imageMin: {
        optimizationLevel: 5,
        progressive: true,
        interlaced: true
    },

    args: function (args, adds) {
        adds = adds || {};
        args = args || {};
        for (i in adds) {
            args[i] = (typeof args[i] != 'undefined' && args[i] != null) ? args[i] : adds[i];
        }
        return args;
    },

    error: function (err) {
        util.log(util.colors.yellow(err));
        util.beep();
    }
};
