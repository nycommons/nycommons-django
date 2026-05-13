module.exports = function(grunt) {
    grunt.initConfig({
        browserify: {
            dev: {
                options: {
                    browserifyOptions: {
                        debug: true
                    },
                    watch: true
                },
                src: 'js/main.js',
                dest: 'js/dist/bundle.dev.js'
            },
            production: {
                options: {
                    watch: true
                },
                src: '<%= browserify.dev.src %>',
                dest: 'js/dist/bundle.js'
            }
        },

        cssmin: {
            options: {
                // Don't rebase urls. This was breaking relative urls.
                rebase: false
            },
            minify: {
                src: '<%= less.production.dest %>',
                dest: 'css/dist/style.min.css'
            }
        },

        jshint: {
            all: {
                files: {
                    src: [
                        'js/*.js',
                        '!<%= browserify.dev.dest %>',
                        '!<%= browserify.production.dest %>',
                        '!<%= uglify.production.dest %>'
                    ]
                }
            }
        },

        less: {
            dev: {
                options: {
                    plugins: [
                        new (require('less-plugin-lists'))
                    ],
                    sourceMap: true,
                    sourceMapFileInline: true
                },
                src: 'css/style.less',
                dest: 'css/dist/style.dev.css'
            },
            production: {
                options: {
                    plugins: [
                        new (require('less-plugin-lists'))
                    ],
                },
                src: '<%= less.dev.src %>',
                dest: 'css/dist/style.css'
            }
        },

        uglify: {
            production: {
                src: '<%= browserify.production.dest %>',
                dest: 'js/dist/bundle.min.js'
            }
        },

        watch: {
            jshint: {
                files: ['js/*.js'],
                tasks: ['jshint']
            },

            less: {
                files: ['css/*.less', 'css/*/*.less'],
                tasks: ['less', 'cssmin']
            },

            uglify: {
                files: ['<%= browserify.production.dest %>'],
                tasks: ['uglify']
            }
        }
    });

    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('dev', ['browserify', 'watch']);
};
