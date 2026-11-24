import {mount} from './base.js';
import {render as material} from './material_page.js';
import {render as caliper} from './caliper_page.js';
import {render as variance} from './variance_page.js';
import {render as release} from './release_page.js';
const pages = {"material": "小样配对", "caliper": "渗透计量", "variance": "嵌套变异", "release": "放行补测"};
const screens = {material, caliper, variance, release};
mount({title: "蜡痕样册 · 织补蜡点渗透变异复核", kicker: "面料室 / 样册和实测", pages, render: (page, outlet, user) => screens[page](outlet, user)});
