module.exports = function(grunt) {
  'use strict';

  require('load-grunt-tasks')(grunt);

  require("grunt-load-gruntfile")(grunt);
  grunt.loadGruntfile("./Gruntfile.js");

  grunt.config.set('watch.scripts.files', [])

  // grunt.config.set(, value)
  grunt.config.merge({
    watch: {
      "webcouturier-dropdownmenu-less": {
        files: ['src/**/*.less'],
        tasks: ["less:webcouturier-dropdownmenu", "sed"]
      },
      "webcouturier-dropdownmenu-js": {
        files: ['src/**/dropdown.js'],
        tasks: ["requirejs:webcouturier-dropdownmenu", "uglify:webcouturier-dropdownmenu", "clean"]
      }
    },
    browserSync: {
      bsFiles: {
        src : [
          'src/**/*-compiled.css',
          'src/**/*-compiled.js',
          'src/**/*.pt'
        ]
      },
      options: {
        watchTask: true,
        debugInfo: true,
        proxy: "localhost:8080",
        open:false,
        injectChanges: true,
        reloadDelay: 0,
        // reloadDebounce: 2000,
        online: true,
        browser: "google chrome"
      }
    },
    clean: {
      js: ['src/**/webcouturier-*.js']
    }
  });

  // grunt.file.setBase('./src/webcouturier/dropdownmenu/static');

  grunt.registerTask('sync', ["browserSync", "watch"]);

};
