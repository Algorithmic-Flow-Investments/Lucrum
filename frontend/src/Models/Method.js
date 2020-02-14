export default class Method {
	constructor(data) {
		this.unpack(data);
	}

	unpack(data) {
		this.id = data.id;
		this.name = data.name || "";
	}
}
