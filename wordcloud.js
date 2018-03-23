var img_pos, element_pos,img_neg, element_neg;
img_pos = document.createElement('img');
img_neg = document.createElement('img');
img_pos.src = "static/wordcloud_pos.png"
img_neg.src = "static/wordcloud_neg.png"
element_pos = document.getElementById("wordcloud_pos");
element_neg = document.getElementById("wordcloud_neg");
element_pos.appendChild(img_pos);
element_neg.appendChild(img_neg);
