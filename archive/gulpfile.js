// Base
const path              = require('path');
const gulp              = require('gulp');
const notify            = require('gulp-notify');
const plumber           = require('gulp-plumber');

// Server
const browserSync 		= require('browser-sync');

// General
const concat            = require('gulp-concat');
const sourcemaps        = require('gulp-sourcemaps');

// Scripts
const webpack           = require('webpack')
const webpackStream     = require('webpack-stream');

// Styles
const sass              = require('gulp-sass');
const autoprefixer      = require('gulp-autoprefixer');
const cssbeautify 		= require('gulp-cssbeautify');

// Images
const tinypng 			= require('gulp-tinypng-compress');
const svgSprite 		= require('gulp-svg-sprites');
const replace 			= require('gulp-replace');
const cheerio 			= require('gulp-cheerio');
const base64 			= require('gulp-base64');

// Jade
const pug = require('gulp-pug');


// Paths
const paths = {
    build:  path.join(__dirname, '.'),
    node:   path.join(__dirname, 'node_modules'),
    src: {
        self:       path.join(__dirname, 'src'),
        js:         'src/js/',
        sass:       'src/scss/',
        images:     'src/images/',
        pug:        'src/jade/',
    },
    static: {
        self:       'static/',
        js:         'static/js/',
        css:        'static/css/',
        images:     'static/images/',
    },
    html: './'
}

gulp.task('browserSync', function () {
	browserSync({ 
		server: { 
			port: 8000,
			baseDir: './',
			directory: true
		}
	});
});

// gulp.task("js", function() {
//     gulp.src(path.join(paths.src.self, "js", "index.js"))
//         .pipe(webpackStream({
//             mode: "development",
//             entry: {
//                 main: path.join(paths.src.self, "js", "index.js")
//             },
//             module: {
//                 rules: [
//                     {
//                         test: /\.(js|jsx)$/,
//                         exclude: /node_modules/,
// 						use: {
// 							loader: 'babel-loader',
// 							options: {
// 							  presets: ['@babel/preset-env'],
// 							}
// 						}
//                     },
//                 ]
//             },
//             resolve: {
//                 extensions: ["*", ".js", ".jsx"],
//                 modules: [
//                     paths.node,
//                     paths.src.self,
//                 ],
//                 alias: {
//                     'jquery': paths.node + '/jquery/dist/jquery.js',
//                 }
//             },
//             output: {
//                 path: paths.build,
//                 publicPath: "/",
//                 filename: "static/js/[name].bundle.js",
//                 library: "[name]"
//             },
//             optimization: {
//                 splitChunks: {
//                     cacheGroups: {
//                         commons: {
//                             test: /[\\/](node_modules|vendors)[\\/]/,
//                             name: "vendors",
//                             chunks: "all"
//                         }
//                     }
//                 }
//             },
//             plugins: [
//                 new webpack.ProvidePlugin({
//                     $: "jquery",
//                     jQuery: "jquery",
//                     "window.$": "jquery",
// 					"window.jQuery": "jquery"
//                 })
//             ]
//         }))
//         .pipe(gulp.dest(paths.build));
// });

gulp.task('js', function() {
    gulp.src(path.join(paths.src.self, "js", "index.js"))
        .pipe(webpackStream({
            mode: "development",
            entry: {
                main: path.join(paths.src.self, "js", "index.js")
			},
			output: {
                path: paths.build,
                publicPath: "/",
                filename: "static/js/[name].bundle.js",
                library: "[name]"
            },
            module: {
                rules: [
                    {
                        test: /\.(js|jsx)$/,
                        exclude: /node_modules/,
                        use: {
							loader: 'babel-loader',
							options: {
							  presets: ['@babel/preset-env'],
							}
						}
                    },
                ]
            },
            resolve: {
                extensions: ["*", ".js", ".jsx"],
                modules: [
                    paths.node,
                    paths.src.self,
                ],
                alias: {
                    'jquery': paths.node + '/jquery/dist/jquery.js',
                }
            },
            optimization: {
                splitChunks: {
                    cacheGroups: {
                        commons: {
                            test: /[\\/](node_modules|vendors)[\\/]/,
                            name: "vendors",
                            chunks: "all"
                        }
                    }
                }
            },
            plugins: [
                new webpack.ProvidePlugin({
                    $: "jquery",
                    jQuery: "jquery",
                    // "window.$": "jquery",
					// "window.jQuery": "jquery"
                })
            ]
        }))
        .pipe(gulp.dest(paths.build));
});

gulp.task('js-build', function() {
    gulp.src(path.join(paths.src.self, "js", "index.js"))
		.pipe(webpackStream({
			mode: "production",
			entry: {
				main: path.join(paths.src.self, "js", "index.js")
			},
			module: {
				rules: [
					{
						test: /\.(js|jsx)$/,
						exclude: /node_modules/,
						use: {
							loader: 'babel-loader',
							options: {
							  presets: ['@babel/preset-env'],
							}
						}
					},
				]
			},
			resolve: {
				extensions: ["*", ".js", ".jsx"],
				modules: [
					paths.node,
					paths.src.self,
				],
				alias: {
					'jquery': paths.node + '/jquery/dist/jquery.js',
				}
			},
			output: {
				path: paths.build,
				publicPath: "/",
				filename: "static/js/[name].bundle.js",
				library: "[name]"
			},
			optimization: {
				splitChunks: {
					cacheGroups: {
						commons: {
							test: /[\\/](node_modules|vendors)[\\/]/,
							name: "vendors",
							chunks: "all"
						}
					}
				}
			},
			plugins: [
				new webpack.ProvidePlugin({
					$: "jquery",
                    jQuery: "jquery",
                    // "window.$": "jquery",
					// "window.jQuery": "jquery"
				})
			]
		}))
		.pipe(gulp.dest(paths.build));
});
  
gulp.task('sass', function () {
    // Libs
	gulp.src([
		path.join(paths.node,       "bootstrap/scss/bootstrap.scss"),
		path.join(paths.node,       "overlayscrollbars/css/OverlayScrollbars.min.css"),
		path.join(paths.node,       "ion-rangeslider/css/ion.rangeSlider.css"),
		path.join(paths.node,       "ion-rangeslider/css/ion.rangeSlider.skinHTML5.css"),
		path.join(paths.node,       "slick-carousel/slick/slick.scss"),
		path.join(paths.node,       "@fancyapps/fancybox/dist/jquery.fancybox.css"),
		path.join(paths.src.sass,   "vendors/*.+(scss|sass)"),
	])
	.pipe(plumber({ errorHandler: notify.onError("<%= error.message %>") }))
	.pipe(sass({outputStyle: "compressed"}).on("error", sass.logError))
	.pipe(autoprefixer("last 2 version"))
	.pipe(concat("vendors.min.css"))
	.pipe(gulp.dest(paths.static.css))


    // Styles
    gulp.src(path.join(paths.src.sass, "main.scss"))
    .pipe(plumber({ errorHandler: notify.onError("<%= error.message %>") }))
    .pipe(sourcemaps.init())
    .pipe(sass().on("error", sass.logError))
    .pipe(base64({
        baseDir: '/static/test',
        extensions: ['svg', 'png', /\.jpg#datauri$/i],
        exclude: [/\.server\.(com|net)\/dynamic\//, '--live.jpg'],
        maxImageSize: 32 * 1024, // bytes 
        debug: false
    }))
	.pipe(autoprefixer("last 2 version"))
	.pipe(cssbeautify({
		indent: '	',
		autosemicolon: true
	}))
	.pipe(sourcemaps.write("./", { sourceRoot: "/src/scss" }))
	// .pipe(gulp.dest(function(file){
	// 	return file.base;
	// }))
    .pipe(gulp.dest(paths.static.css))
});

gulp.task('sass-build', function () {
    // Styles
    gulp.src(path.join(paths.src.sass, "main.scss"))
    .pipe(plumber({ errorHandler: notify.onError("<%= error.message %>") }))
    .pipe(sass({outputStyle: "compressed"}).on("error", sass.logError))
    .pipe(base64({
        baseDir: '/static/test',
        extensions: ['svg', 'png', /\.jpg#datauri$/i],
        exclude: [/\.server\.(com|net)\/dynamic\//, '--live.jpg'],
        maxImageSize: 32 * 1024, // bytes 
        debug: false
    }))
    .pipe(autoprefixer("last 2 version"))
    .pipe(gulp.dest(paths.static.css))
});

gulp.task('tinypng', function () {
	gulp.src(paths.src.images + '/*.{png,jpg,jpeg}')
	.pipe(tinypng({
		key: 'odthLyLlVCQlfl9KLbpWcDBGEAqaBK8T',
		sigFile: paths.static.images + '/.tinypng-sigs'
	}))
	.pipe(gulp.dest(paths.static.images))
});

gulp.task('svg', function () {
	gulp
		.src(paths.src.images + '/*.svg')
		.pipe(cheerio({
            run: function ($) {
                $('[fill]').removeAttr('fill');
                $('[style]').removeAttr('style');
            },
			parserOptions: { xmlMode: true }
        }))
        .pipe(replace('&gt;', '>'))
        .pipe(
            svgSprite({
                mode: "symbols",
                preview: false,
                selector: "%f",
                svg: {
                symbols: 'sprite.svg' 
            },
            transformData: function (data, config) {
                for(var i in data.svg) {
                    var result = data.svg[i].data.match(/path id="([a-z]+)"/ig );
                    if (null !== result) {
                        for(var j in result) {
                            var regexp = /\"([a-z]+)\"/i;
                            var matches = regexp.exec(result[j]);
                            matches[0] = matches[0].replace(/\"/g, '');

                            var k = 0;

                            var regexp = new RegExp('(path id\=\"|xlink\:href\=\"#)('+matches[0]+'){1}', 'g');
                            data.svg[i].data = data.svg[i].data.replace(regexp, function(str, p1, p2, offset, s)
                                {
                                    return p1 + "" + i + "" + j + "" + p2;
                                });
                        }
                    }
                }
                return data;
            },
        }
        ))
        .pipe(replace('NaN ', '-'))
        .pipe(gulp.dest(paths.static.images))
});

gulp.task('static-svg', function () {
	gulp
		.src(paths.src.images + '/static/*.svg')
        .pipe(replace('&gt;', '>'))
        .pipe(
            svgSprite({
                mode: "symbols",
                preview: false,
                selector: "%f",
                svg: {
                symbols: 'static-sprite.svg' 
            },
            transformData: function (data, config) {
                for(var i in data.svg) {
                    var result = data.svg[i].data.match(/path id="([a-z]+)"/ig );
                    if (null !== result) {
                        for(var j in result) {
                            var regexp = /\"([a-z]+)\"/i;
                            var matches = regexp.exec(result[j]);
                            matches[0] = matches[0].replace(/\"/g, '');

                            var k = 0;

                            var regexp = new RegExp('(path id\=\"|xlink\:href\=\"#)('+matches[0]+'){1}', 'g');
                            data.svg[i].data = data.svg[i].data.replace(regexp, function(str, p1, p2, offset, s)
                                {
                                    return p1 + "" + i + "" + j + "" + p2;
                                });
                        }
                    }
                }
                return data;
            },
        }
        ))
        .pipe(replace('NaN ', '-'))
        .pipe(gulp.dest(paths.static.images))
});

gulp.task('pug', function () {
	gulp
		.src(paths.src.pug + '/*.pug')
		.pipe(plumber({ errorHandler: notify.onError("<%= error.message %>") }))
		.pipe(pug({pretty: '\t'}))
		.pipe(gulp.dest(paths.html))
})

gulp.task('watch', function () {
    gulp.watch(paths.src.pug    + '/*.pug', ['pug']);
    
    gulp.watch(paths.src.js     +  '**/*.+(js|ts)', ['js']);
    gulp.watch(paths.src.sass   +  '**/*.+(scss|sass)', ['sass']);
    
	gulp.watch(paths.src.images + '/*.{png,jpg,jpeg}', ['tinypng']);
	gulp.watch(paths.src.images + '**/*.svg', ['svg', 'static-svg']);
});


gulp.task('default', ['watch', 'pug', 'js', 'sass', 'tinypng', 'svg', 'static-svg', 'browserSync']);
gulp.task('build', ['js-build', 'sass-build']);