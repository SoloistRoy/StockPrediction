module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		concat: {
		    dist: {
		      src: ['node_modules/jquery/dist/jquery.min.js','node_modules/bootstrap/dist/js/bootstrap.min.js','js/**','!js/app.js'],
		      dest: 'public/js/app.js',
		    }
		},
		watch: {
			options: {
				livereload: true
			},
			scripts: {
				files: ['public/js/**','!js/app.js'],
				tasks: ['concat']
			},
			bootstrap: {
				files: ['public/less/**'],
				tasks: ['less','cssmin']
			},
			templates: {
				files: ['public/partials/*']
			},
			index: {
				files: ['index.html']
			}
		},
		cssmin: {
			target: {
				files: [{
					expand: true,
					cwd: 'public/css/',
					src: 'styles.css',
					dest: 'public/css/',
					ext: '.min.css'
				}]
			}
		},
		connect: {
			server: {
				options: {
					livereload: true,
					open: true,
					hostname: 'localhost'
				}
			}
		},
		less: {
			compileCore: {
		        options: {
		          strictMath: true
		        },
		        src: 'public/less/styles.less',
		        dest: 'public/css/styles.css'
			}
		},
		cacheBust: {
			options: {
				assets: ['assets/**/*'],
				baseDir: './public/'
			},
			taskName: {
				files: [{   
					expand: true,
					cwd: 'public/',
					src: ['public/partials/*.html', 'assets/**/*']
				}]
			}
		},
		assets: {
			options: {
				baseDir: 'public/',
			},
			files: [{   
				expand: true,
				cwd: 'public/',
				src: ['public/**/*.html']
			}]
		}
	});

	grunt.registerTask('server', ['concat','less','cssmin','connect','watch']);
	grunt.registerTask('default', ['concat','less','cssmin', 'watch']);

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-connect');
	grunt.loadNpmTasks('grunt-contrib-less');
};
