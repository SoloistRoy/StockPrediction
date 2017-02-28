module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		concat: {
		    dist: {
		      src: ['node_modules/jquery/dist/jquery.min.js','node_modules/bootstrap/dist/js/bootstrap.min.js','js/**','!js/app.js'],
		      dest: 'js/app.js',
		    }
		},
		watch: {
			options: {
				livereload: true
			},
			scripts: {
				files: ['js/**','!js/app.js'],
				tasks: ['concat']
			},
			bootstrap: {
				files: ['less/**'],
				tasks: ['less','cssmin']
			},
			templates: {
				files: ['templates/*']
			},
			index: {
				files: ['index.html']
			}
		},
		cssmin: {
			target: {
				files: [{
					expand: true,
					cwd: 'css/',
					src: 'styles.css',
					dest: 'css/',
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
		        src: 'less/styles.less',
		        dest: 'css/styles.css'
			}
		}
	});

	grunt.registerTask('server', ['concat','less','cssmin','connect','watch']);
	grunt.registerTask('default', ['concat','less','cssmin']);

	grunt.loadNpmTasks('grunt-contrib-concat');
	grunt.loadNpmTasks('grunt-contrib-watch');
	grunt.loadNpmTasks('grunt-contrib-cssmin');
	grunt.loadNpmTasks('grunt-contrib-connect');
	grunt.loadNpmTasks('grunt-contrib-less');
};
