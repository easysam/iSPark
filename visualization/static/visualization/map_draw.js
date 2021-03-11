function draw_edit_road(status, result) {
    if (status === 'complete') {
        console.log('Complete searching, the road is drawn.')
    }
    else {
        console.log('Can\'t find this road');
        return;
    }
    for (let i = 0; i < result.roadInfo.length; i++) {
        const element = result.roadInfo[i];
        for (let j = 0; j < element.path.length; j++) {
            const path = element.path[j];
            const polyline = new AMap.Polyline({
                path: path,
                borderWeight: 5, // 线条宽度，默认为 1
                strokeColor: 'green', // 线条颜色
                lineJoin: 'round', // 折线拐点连接处样式
                draggable: true
            });
            map.add(polyline)
        }
    }
    map.setFitView();
}