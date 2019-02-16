    // Array

    // String
   String.prototype.replaceAll = function(target, replacement) {
      return this.split(target).join(replacement);
    };

    // Date
    Date.prototype.format = function (f) {
        if (!this.valueOf()) return " ";
        var weekName = ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일"];
        var d = this;

        return f.replace(/(yyyy|yy|MM|dd|E|hh|mm|ss|a\/p)/gi, function ($1) {
            switch ($1) {
                case "yyyy": return d.getFullYear();
                case "yy": return (d.getFullYear() % 1000).zf(2);
                case "MM": return (d.getMonth() + 1).zf(2);
                case "dd": return d.getDate().zf(2);
                case "E": return weekName[d.getDay()];
                case "HH": return d.getHours().zf(2);
                case "hh": return ((h = d.getHours() % 12) ? h : 12).zf(2);
                case "mm": return d.getMinutes().zf(2);
                case "ss": return d.getSeconds().zf(2);
                case "a/p": return d.getHours() < 12 ? "오전" : "오후";
                default: return $1;
            }
        });
    };

    String.prototype.string = function (len) { var s = '', i = 0; while (i++ < len) { s += this; } return s; };
    String.prototype.zf = function (len) { return "0".string(len - this.length) + this; };
    Number.prototype.zf = function (len) { return this.toString().zf(len); };


var MINUTE_BY_SEC = 60 * 1000;
var HOUR_BY_SEC = 60 * MINUTE_BY_SEC;
var DAY_BY_SEC = 24 * HOUR_BY_SEC;

var JSUtils = {
    /**
     * 오브젝트 dom 맵핑
     * param dom_id : DOM id
     * tmpl_id : 템플릿 id
     * obj : 오브젝트
     * isAppend : append 붙여쓰기 여부 (기본 false)
     */
    generateTemplate : function( dom_id, tmpl_id, obj, isAppend ){
        var element = document.getElementById( dom_id );
        if ( element ){

            if( isAppend ){
                element.innerHTML = element.innerHTML + tmpl( tmpl_id, { obj : obj } );
            }
            else{
                element.innerHTML = tmpl( tmpl_id, { obj : obj } );
            }
        }
    },

    decodeHtml : function (html) {
        var txt = document.createElement("textarea");
        txt.innerHTML = html;
        return txt.value;
    },

    getObjectFromJson : function ( json, usingNormalize ){

        var decodeJson = this.decodeHtml( json )
        if ( usingNormalize ){
            var normalizeJson = decodeJson.replaceAll( "(\"", "(\'").replaceAll( "\")", "\')");
            return JSON.parse( normalizeJson );
        }
        return JSON.parse( decodeJson );
    },

    /**
     *  현재 시간 기준으로, 시간차 텍스트 조회
     *  @param dt : datetime (yyyy-MM-dd HH:mm:ss)
     *  @return : N일 전, N시간 전, N분 전
     **/
    getTimeGapFmt : function( dt ){

        var now = new Date();
        var itemDate = new Date( dt );
        var timeDiff = now.getTime() - itemDate.getTime();

        if ( timeDiff > DAY_BY_SEC ){
            return ( Math.ceil(timeDiff/ DAY_BY_SEC) - 1   ) + '일전';
        }
        else if ( timeDiff > HOUR_BY_SEC ){
            return ( Math.ceil(timeDiff/ HOUR_BY_SEC) - 1 ) + '시간전';
        }
        return ( Math.ceil(timeDiff/ MINUTE_BY_SEC) - 1 ) + '분전';
    }
}