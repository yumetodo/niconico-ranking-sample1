// License: Boost Software License 1.0
// See https://www.boost.org/LICENSE_1_0.txt
// Copyright © 2018 yumetodo <yume-wikijp@live.jp>
(function(){
    // const endpoint_url = new URL("https://api.search.nicovideo.jp/api/v2/snapshot/video/contents/search");
    // const query_args = Object.freeze({
    //     'q':'初音ミク',
    //     "targets":"title",
    //     "fields":"contentId,title,viewCounter,commentCounter,mylistCounter",
    //     "filters[viewCounter][gte]":"10000",
    //     "_sort":"-viewCounter",
    //     "_offset":"0",
    //     "_limit":"100",
    //     "_context":"name"
    // });
    const error_code_conv_table = Object.freeze({
        400: "不正なパラメータです",
        500: "検索サーバの異常です",
        503: "サービスがメンテナンス中です"
    });
    // Object.keys(query_args).forEach(key => endpoint_url.searchParams.append(key, query_args[key]));
    function ready(loaded) {
        if (['interactive', 'complete'].includes(document.readyState)) {
            loaded();
        } else {
            document.addEventListener('DOMContentLoaded', loaded);
        }
    }
    // fetch(endpoint_url, {"mode": "cors", "headers": new Headers({"Content-Type": "text/json"})})
    fetch("miku.json")
    .then(r => r.json()).then(response => {
        const status = response["meta"]["status"];
        if(200 !== status){
            ready(() => {
                document.body.innerText = (status in error_code_conv_table)
                    ? `code: ${status} \n${error_code_conv_table[status]}`
                    : `code: ${status}`;
            });
        }
        else {
            const ranking = response["data"].map(d => m("section", {"class": "box"}, [
                m("img", {"src": `https://tn.smilevideo.jp/smile?i=${d["contentId"].slice(2)}`}),
                m("p", {"class": "text"}, `${d["title"]}`),
                m("div", {"class": "point"}, [
                    m("p", {"class": "point1"}, [
                        m("div", {"class": "point2"}, "再生数"),
                        m("div", {"class": "point3"}, "コメント"),
                        m("div", {"class": "point3"}, "マイリス")
                    ]),
                    m("p", {"class": "point1"}, [
                        m("div", {"class": "point4"}, `${d["viewCounter"]}`),
                        m("div", {"class": "point5"}, `${d["mylistCounter"]}`),
                        m("div", {"class": "point5"}, `${d["commentCounter"]}`)
                    ])
                ]),
            ]));
            ready(() => {
                m.mount(document.getElementById("menu01"), { view: () => ranking});
            });
        }
    }).catch(reason => {
        ready(() => {
            document.body.innerText = reason.toString();
        });
    });
})();
