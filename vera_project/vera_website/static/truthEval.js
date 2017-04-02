 $(function() {
        const params = {
            // Request parameters
            "model": "body",
            "order": "5"
        };
      
        $.ajax({
            url: "https://westus.api.cognitive.microsoft.com/text/weblm/v1.0/calculateJointProbability?" + $.param(params),
            beforeSend: function(xhrObj){
                // Request headers
                xhrObj.setRequestHeader("Content-Type","application/json");
                xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key","a58917402b924e17a2fb312cc7f4df30");
            },
            type: "POST",
            // Request body
            data: '{"queries":["test if this is true"]}',
        })
        .done(function(data) {
            alert("success");
            let truthProb = data["results"][0]["probability"];
            let outputText = '<p><img src="https://media3.giphy.com/media/uP89pJyXBDqVi/giphy.gif"></p><p>Probably false.</p>'
            if (truthProb > -10.0) {
                outputText = '<p><img src="http://images.techtimes.com/data/images/full/163412/falloutvaultboythumbsup.jpg"></p><p>Probably true.</p>'
            }
            document.getElementById("shnitzel").innerHTML = outputText
        })
        .fail(function() {
            alert("error");
        });
    });