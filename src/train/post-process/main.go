package main

import (
	"gitlab.intelygenz.com/konstellation-io/kai/kai-gosdk/runner"
	"gitlab.intelygenz.com/konstellation-io/kai/kai-gosdk/sdk"
	"google.golang.org/protobuf/types/known/anypb"
)

func initializer(kaiSDK sdk.KaiSDK) {
	kaiSDK.Logger.Info("Initializing example..")
}

func handler(kaiSDK sdk.KaiSDK, msg *anypb.Any) error {
	kaiSDK.Logger.Info("Received message example", "msg", msg.Value)

	kaiSDK.Messaging.SendAny(msg)

	return nil
}

func finalizer(kaiSDK sdk.KaiSDK) {
	kaiSDK.Logger.Info("Finalizing example..")
}

func main() {
	runner.
		NewRunner().
		TaskRunner().
		WithInitializer(initializer).
		WithHandler(handler).
		WithFinalizer(finalizer).
		Run()
}
