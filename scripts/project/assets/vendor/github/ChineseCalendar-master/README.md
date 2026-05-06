# Conversion between Western and Chinese Calendar (722 BCE - 2200 CE) 
# 公 曆 和 農 曆 日 期 對 照 (公元前722年- 公元2200年)

This package contains HTML files, javascript files, and pdf documentation.

The [main page](https://ytliu0.github.io/ChineseCalendar/) uses my calculated calendar data to convert between the Western calendar and Chinese calendar for any year between 722 BCE and 2200 CE (CE = [Common Era](https://en.wikipedia.org/wiki/Common_Era)). The other pages are linked at the top of the main page. They are self-explanatory. 

## Installation from Source Files

The pre-built version (all HTML files, figures, css, js and pdf files in `.` and `./docs` directory) is intended for public use only, but you can install another version for private use from the build script. 

### Quick Installation 

To install the whole package to a target directory, first open `build_config.json` and edit the value of the `"target directory"` key. For first time installation, run `npm install` to install dependencies. Then run `npm run build` or `node build.js all` to install the package in the target directory. Use `npm run clean` or `node build.js clean` to remove the target directory.

Note that the target directory cannot be the same as the source directory `./src` since some of the output files will have the same names as the files in the source directory. To prevent accidental overwriting of source files, a file named `protect_this_dir.txt` is placed in the source directory. If the build script detects the existence of this filename in the target directory, it will abort and throw an error.

### Customized Build (for development)

The command `npm run build` or `node build.js all` installs the whole package from scratch. If only a few files are modified, it's not necessary to rebuild everything. In this case, you can change the parameters in `build_config.json` before running the build script. Apart from the `target_directory` key, values of all the other keys in `build_config.json` are boolean. In the command `npm run part` or `node build.js`, only items that are `true` in `build_config.json` will be built. You can also specify another json file for `build.js` to process. For example, `node build.js my_config.json` will read `my_config.json` instead of `build_config.json`. In other words, if the second argument after `node` is not `all` and `clean`, it will be interpreted as a json file for configuration.

