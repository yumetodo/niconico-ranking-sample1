// License: Boost Software License 1.0
// See https://www.boost.org/LICENSE_1_0.txt
// Copyright © 2018 yumetodo <yume-wikijp@live.jp>

const fs = require("fs");
const URL = require('url').URL;
const fetch = require('node-fetch');

const endpoint_url = new URL("https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search");
const query_args = Object.freeze({
    'q':'初音ミク',
    "targets":"title",
    "fields":"contentId,title,viewCounter,commentCounter,mylistCounter",
    "filters[viewCounter][gte]":"10000",
    "_sort":"-viewCounter",
    "_offset":"0",
    "_limit":"100",
    "_context":"name"
});
Object.keys(query_args).forEach(key => endpoint_url.searchParams.append(key, query_args[key]));
(async function() {
    console.log("start updating...")
    const res = await fetch(endpoint_url.toString()).then(r => r.text());
    fs.writeFileSync("miku.json", res, "utf-8");
    console.log("update success.")
})();
