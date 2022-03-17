#!/bin/bash


CrawlerPath="core/crawler/ext"
SubFinderPath="core/recon/subenum/subfinder/ext"
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
    export GOROOT=/usr/local/go
    export GOPATH=$home/go
    export PATH=$GOPATH/bin:$GOROOT/bin:$home/.local/bin:$PATH

    cat <<- EOF >> $home/.profile
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
    isFileExist "$CrawlerPath/RockRawler.a" || isFileExist "$CrawlerPath/RockRawler.h"
}

SetupRockRawler() {
    print_status "Build RockRawler extension"

    if ! IsRockRawlerExtInstalled; then
        cd "$CrawlerPath/RockRawler"
        go build -o ../ -buildmode=c-archive RockRawler.go &>/dev/null
        cd "$CurrPath"

        if IsRockRawlerExtInstalled; then
            print_succeed "RockRawler built successfully"
        else
            print_fail "RockRawler Build Failed"
            exit 1
        fi

    else
        print_indicate "RockRawler extension has already been built before"
    fi
}

SetupCrawlerLib() {
    print_status "Setup Crawler Library"

    if ! isDirExist "$CrawlerPath/build"; then
        cd $CrawlerPath
        python3 setup.py build &>/dev/null
        python3 setup.py install &>/dev/null
        cd "$CurrPath"

        if isDirExist "$CrawlerPath/build"; then
            print_succeed "Crawler lib built successfully"

        else
            print_fail "an error occured"
            print_indicate "Please reinstall or run 'cd $CrawlerPath; python3 setup.py build; python3 setup.py install'"
            exit 1
        fi
   
    else
        print_indicate "CrawlerLib Already installed"
    fi
}

SetupCrawler() {
    SetupRockRawler
    SetupCrawlerLib
}

IsSubFinderExtInstalled() {
    isFileExist "$SubFinderPath/subfinder.a" || isFileExist "$SubFinderPath/subfinder.h"
}

BuildSubFinder() {
    print_status "Build SubFinder extension"

    if ! IsSubFinderExtInstalled; then
        cd "$SubFinderPath"
        go build -buildmode=c-archive subfinder.go &>/dev/null
        cd "$CurrPath"

        if IsSubFinderExtInstalled; then
            print_succeed "SubFinder built successfully"

        else
            print_fail "SubFinder Build Failed"
            exit 1
        fi

    else
        print_indicate "SubFinder extension has already been built before"
    fi
}

SetupSubFinderLib() {
    print_status "Setup SubFinder Library"

    if ! isDirExist "$SubFinderPath/build"; then
        cd "$SubFinderPath"
        python3 setup.py build &>/dev/null
        python3 setup.py install &>/dev/null
        cd "$CurrPath"

        if isDirExist "$SubFinderPath/build"; then
            print_succeed "SubFinderPath lib built successfully"

        else
            print_fail "an error occured"
            print_indicate "Please reinstall or run 'cd $SubFinderPath && python3 setup.py build && python3 setup.py install' and show the error"
            exit 1
        fi

    else
        print_indicate "SubFinderLib Already installed"
    fi
}

SetupSubFinder() {
    BuildSubFinder
    SetupSubFinderLib
}

SetupSubDomainTools() {
    SetupSublist3r
    SetupSubFinder
}

if [ "$EUID" -ne 0 ]; then 
    print_fail "Please run as root"
    exit 1
fi


SetupEssentialPackages

SetupGoIfDoesNotExist

SetupPyDependencies

SetupCrawler

SetupSubDomainTools

print_succeed "WebRock setup completed successfully"
