export default class Category {
	constructor(data) {
		this.unpack(data);
	}

	unpack(data) {
		this.id = data.id;
		this.name = data.name || "";
	}
}
