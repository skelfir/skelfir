
serve:
	npm run dev

build-vite:
	# https://capacitorjs.com/docs/cli/commands/build
	npm run build

build-docker:
	docker build -t skelfir-app:latest .

build: build-vite build-docker

sync:
	npx cap sync

run-android:
	npx cap run android --target 24201FDF60065K

android: build sync
	npx cap run android --target 24201FDF60065K

logs:
	$$ANDROID_HOME/platform-tools/adb logcat | grep Capacitor/Console
