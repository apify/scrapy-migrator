const { spawnSync } = require('child_process');
const ConfigParser = require('configparser');
const { readdirSync } = require('fs');
const path = require('path');

const { SpiderFileAnalyzer } = require('./SpiderFileAnalyzer');

/**
 * A simple example of analyzing the scrapy project.
 */
class ProjectAnalyzer {
    configuration = null;
    settings = null;

    constructor(pathname) {
        this.pathname = pathname;
        this.loadScrapyCfg();
        this.loadSettings();
    }

    loadScrapyCfg() {
        const config = new ConfigParser();
        config.read(path.join(this.pathname, 'scrapy.cfg'));
        this.configuration = config;
    }

    loadSettings(){
        const pythonProcess = spawnSync('python', [
            path.join(__dirname, 'parseSettings.py'),
            path.join(this.pathname, `${this.configuration.get('settings', 'default').replace('.', '/')}.py`),
        ]);
        const result = pythonProcess.stdout?.toString()?.trim();

        if(pythonProcess.status !== 0) {
            const e = new Error(`There was an error while parsing the settings file.

${pythonProcess.stderr?.toString()}`);

            throw e;
        }

        this.settings = JSON.parse(result);
    }

    getName() {
        return this.settings?.BOT_NAME;
    }

    getAvailableSpiders() {
        const spiderPaths = this.settings?.SPIDER_MODULES;

        if (!spiderPaths) {
            throw new Error('SPIDER_MODULES path not found in settings.');
        }

        const spiders = [];

        for (const spiderPath of spiderPaths) {
            const files = readdirSync(path.join(this.pathname, spiderPath.replace('.', '/')), { withFileTypes: true });
            for (const file of files) {
                if(file.isFile() && file.name.endsWith('.py') && file.name !== '__init__.py') 
                    spiders.push(...(new SpiderFileAnalyzer(path.join(this.pathname, spiderPath.replace('.', '/'), file.name)).getSpiders()));
            }
        }

        return spiders;
    }
}

module.exports = { ProjectAnalyzer };