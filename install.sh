#!/bin/bash


GoRockPath="gorock"
CurrPath=$(pwd)


# Colors used in printing
Green="\033[0;32m"
Blue="\033[0;34m"
Bold="\033[1m"
Red="\033[0;31m"
NC="\033[0m" # No Color


# use -e flag in print functions to allow backslash escape 
print_succeed() {
    echo -e "- * -  ${Green}${1}${NC}"
}

print_status() {
    echo -e "- * -  ${Blue}${1}${NC}"
}

print_fail() {
    echo -e "- * -  ${Red}${1}${NC}"
}

print_indicate() {
    echo -e "- * -  ${Bold}${1}${NC}"
}

isFileExist() {
    [ -f $1 ];
}

isDirExist() {
    [ -d "$1" ]
}

isCommandExist() {
    # return true if the command exist

    [ ! -z $(command -v $1) ]
}

isMac() {
    [[ "$OSTYPE" == "darwin"* ]]
}

isDebian() {
    isFileExist "/etc/debian_version"
}

isRedhat() {
    isFileExist "/etc/redhat-release"
}

isArch() {
    isFileExist "/etc/arch-release"
}

InstallUsingAPT() {
    apt update -y &>/dev/null
    apt install python3 python3-dev python3-pip build-essential gcc -y &>/dev/null
}

InstallUsingYum() {
    yum groupinstall "Development Tools" -y &>/dev/null
    yum install python3 python3-pip python3-devel gcc -y &>/dev/null
}

InstallUsingPacman() {
    pacman -Sy install python python-pip base-devel gcc -y &>/dev/null
}

InstallUsingBrew() {
    if brew --version &>/dev/null; then
	    print_indicate "Brew is already installed"

    else
        print_status "Try to install brew "
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    brew update &>/dev/null
    brew install bash coreutils python python3-dev gcc &>/dev/null
}

SetupEssentialPackages() {
    print_status "Setup essential packages"

    if isDebian; then
        InstallUsingAPT

    elif isRedhat; then
        InstallUsingYum

    elif isArch; then
        InstallUsingPacman

    elif isMac; then
        InstallUsingBrew
    fi
}

InstallGolang() {
    rm -rf /usr/local/go

    if isMac; then
        wget https://go.dev/dl/go1.17.8.darwin-amd64.tar.gz -O golang.tar.gz &>/dev/null

    else
        wget https://go.dev/dl/go1.17.8.linux-amd64.tar.gz -O golang.tar.gz &>/dev/null    
    fi


    tar -C /usr/local -xzf golang.tar.gz &>/dev/null
    rm golang.tar.gz
    ln -sf /usr/local/go/bin/go /usr/local/bin/

} 

AddGoToProfile() {
    user=$(who am i | awk '{print $1}')
    home=$(eval echo ~$user)
    profile=".$(basename $(echo $SHELL))rc"

    export GOROOT=/usr/local/go
    export GOPATH=$home/go
    export PATH=$GOPATH/bin:$GOROOT/bin:$home/.local/bin:$PATH

    cat <<- EOF >> $home/$profile
		# Golang vars
		export GOROOT=/usr/local/go
		export GOPATH=\$HOME/go
		export PATH=\$GOPATH/bin:\$GOROOT/bin:\$HOME/.local/bin:\$PATH
	EOF

}

SetupGoIfDoesNotExist() {
    if ! isCommandExist "go"; then
        print_fail "Golang does not exist !!"
        print_status "Install Golang"
        InstallGolang
        
        if isCommandExist "go"; then
            print_succeed "Golang installed successfully"
            AddGoToProfile
            print_succeed "Golang added to bash profile"

        else
            print_fail "Golang install Failed !!"
            print_indicate "Please try to install golang manual and reinstall again"
            exit 1
        fi

    else
        print_indicate "Golang Already installed"
    fi
}

SetupSublist3r() {
    print_status "Setup sublist3r Dependencies and Libraries"
    cd "core/recon/subenum/sublist3r/"
    pip3 install -r requirements.txt &>/dev/null
    print_succeed "Sublist3r Setup completed successfully"
    cd "$CurrPath"
}

SetupPyDependencies() {
    print_status "Setup WebRock Dependencies and Libraries"
    pip3 install -r requirements.txt &>/dev/null
    print_succeed "Setup completed successfully"
}

IsRockRawlerExtInstalled() {
    isFileExist "$GoRockPath/ext/RockRawler.a" || isFileExist "$GoRockPath/ext/RockRawler.h"
}

BuildRockRawler() {
    print_status "Build RockRawler"

    if ! IsRockRawlerExtInstalled; then
        cd "$GoRockPath/src/RockRawler"
        go build -o ../../ext -buildmode=c-archive RockRawler.go &>/dev/null
        cd "$CurrPath"

        if IsRockRawlerExtInstalled; then
            print_succeed "RockRawler built successfully"
            
        else
            print_fail "RockRawler Build Failed"
            exit 1
        fi

    else
        print_indicate "RockRawler has already been built before"
    fi
}

IsSubFinderExtInstalled() {
    isFileExist "$GoRockPath/ext/subfinder.a" || isFileExist "$GoRockPath/ext/subfinder.h"
}

BuildSubFinder() {
    print_status "Build SubFinder"

    if ! IsSubFinderExtInstalled; then
        cd "$GoRockPath/src/subfinder"
        go build -o ../../ext -buildmode=c-archive subfinder.go &>/dev/null
        cd "$CurrPath"

        if IsSubFinderExtInstalled; then
            print_succeed "SubFinder built successfully"

        else
            print_fail "SubFinder Build Failed"
            exit 1
        fi

    else
        print_indicate "SubFinder has already been built before"
    fi
}

SetupGoRockExtensions() {
    print_status "Setup GoRock Framework Extensions"

    if ! isDirExist "$GoRockPath/build"; then
        cd $GoRockPath
        python3 setup.py install &>/dev/null
        cd "$CurrPath"

        if isDirExist "$GoRockPath/build"; then
            print_succeed "GoRock Framework built successfully"

        else
            print_fail "an error occured"
            print_indicate "Please reinstall or run 'cd $GoRockPath; python3 setup.py install'"
            exit 1
        fi
   
    else
        print_indicate "GoRock Extensions Already installed"
    fi
}

BuildGoRockFramework() {
    print_status "Build GoRock Framework"
    BuildRockRawler
    BuildSubFinder
    SetupGoRockExtensions
}


if [ "$EUID" -ne 0 ]; then 
    print_fail "Please run as root"
    exit 1
fi


SetupEssentialPackages

SetupGoIfDoesNotExist

SetupPyDependencies

BuildGoRockFramework

SetupSublist3r

print_succeed "WebRock setup completed successfully"
