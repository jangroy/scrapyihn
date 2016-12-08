/**
 * Created by dave on 08/12/16.
 *
 * Example of script
 */

function run(items) {
    console.log('sorting by timestamp!');
    return _.sortBy(items, ['timestamp']);
    // return _.sortBy(items, function (item) {
    //     return -item.timestamp;
    // });
}

module.exports = {
    run: run
};